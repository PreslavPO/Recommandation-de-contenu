const JSON5 = require("json5");
const process = require("process");

/**
 * Convert an incorrect JSON string to a JSON object
 * @param {string} str String to convert
 * @returns {object} A valid JSON
 */
const strToJSON = (str) => {
	let newStr = str.replace(/None/g, null);
	return JSON5.parse(newStr);
};

/**
 * Replace a character in a string with another one
 * @param {string} str String to replace the character from
 * @param {number} index Position of the character to replace
 * @param {string} char New character in the string
 * @returns {string} The initial string with the character replaced
 */
const setCharAt = (str, index, char) => {
	if (index > str.length - 1) return str;
	return str.substring(0, index) + char + str.substring(index + 1);
};

/**
 * Take the document field (content must be a string) corresponding to the parameter and convert it to JSON
 * @param {string} param name of the field which will be converted
 * @returns {object} Object with the name of the field selected and the new value
 */
const convertListToJSON = (doc, param) => {
	// If we have the parameter is a string
	if (typeof doc[param] === "string" || doc[param] instanceof String) {
		let newVal = null;
		// If the string is empty we convert into JSON else we return null
		if (doc[param].length != 0) {
			newVal = strToJSON(doc[param]);
		}
		return { [param]: newVal };
	}
	return {};
}

/**
 * Convert seconds to a formated string
 * @param {int} totalSeconds seconds that will be converted
 * @returns String in the format minutes:seconds (e.g. 12:55)
 */
const secondsToString = (totalSeconds) => {
	const minutes = ~~((totalSeconds % 3600) / 60); //~~ <=> Math.floor
	const seconds = ~~totalSeconds % 60;
	return ((minutes > 0) ? minutes + ":" : "") + ((minutes >= 1 && seconds < 10) ? "0" : "") + seconds;
}

/**
 * Convert fields of a document to JSON and push this operation to a list of Bulk operations (for executing it later)
 * @param {object} doc The document object where the operation is operated
 * @param {object[]} list The list of Bulk operations where the operation will be
 * @param  {...string} objects all of field names that need to be converted to a JSON
 */
const makeBulkOperations = (doc, list, ...objects) => {
	objects = objects.map(param => convertListToJSON(doc, param));

	list.push({
		"updateOne": {
			"filter": { "_id": doc._id },
			"update": { "$set": Object.assign(...objects) }
		}
	});
}

const convertAllStringToJSON = (database, ...objects) => {
	let totalSize = database.aggregate([
		{ $match: { id: { $type: "int" } } },
		{ $count: "count" },
	]).next().count;
	let showEach = Math.floor(totalSize / 20);

	let bulkOperations = [];
	let counter = 0;
	let startTime = new Date();
	let endTime;

	// Variables for the progress bar
	let progressBar = "|" + "░".repeat(~~(totalSize/showEach)) + "|"
	let progressCounter = 0;

	// Remove cursor on the console
	process.stdout.write("\x1B[?25l");

	// Start operations
	database.find({ id: { $type: "int" } }).forEach((doc) => {
		makeBulkOperations(
			doc,
			bulkOperations,
			...objects
		);
		counter++;
	
		// Affiche des informations pendant le traitements
		if (counter % showEach == 0) {
			database.bulkWrite(bulkOperations, { w: 1 });
			bulkOperations = [];
	
			// Time elapsed since beginning of the forEach
			endTime = new Date();
			let totalSeconds = Math.round((endTime - startTime) / 1000);
	
			// Print the progress of the process
			process.stdout.clearLine(1);
			process.stdout.cursorTo(0);
			progressBar = setCharAt(progressBar, progressCounter+1, "▓");
			progressCounter++;
			process.stdout.write(`Converting string to object : ${progressBar} ${counter} / ${totalSize} | Time elapsed : ${secondsToString(totalSeconds)}`);
		}
	});
	
	// Traite les données qui restent
	if (counter % showEach == 0)
		database.bulkWrite(bulkOperations, { w: 1 });
	
	process.stdout.clearLine(0);
	process.stdout.cursorTo(0);
	process.stdout.write(`Converting string to object : ${progressBar} ${counter} / ${totalSize} | Done !\n`)
	process.stdout.write("\x1B[?25h"); // Put back the cursor on the console
}

print("--- MOVIES ---")
convertAllStringToJSON(
	db.movies, 
	"belongs_to_collection",
	"genres",
	"production_companies",
	"production_countries",
	"spoken_languages",
);

// Show incorrect data
let docsDataMissing = db.movies.aggregate([
	{
		$match: { $or: [
			{ video: {$exists: false} },
			{ release_date: {$exists: false} },
			{ release_date: {$eq: ""} },
			{ id: { $not: { $type: "int" } } },
		]}
	}
])
let missingValue = [];
docsDataMissing.forEach(e => missingValue.push(e._id.toString()));
print("\nMovies's id with incorrect or missing values (" + missingValue.length + " documents) :")
print(missingValue)

print("Converting fields to corresponding type ...")
db.movies.updateMany(
	{
		video: { $exists: false },
		release_date: { $exists: false, $ne: "" },
		id: { $type: "int" },
	},
	[{
		$set: {
			adult: {
				$cond: { if: { $eq: ["$adult", "True"] }, then: true, else: false }
			},
			video: {
				$cond: { if: { $eq: ["$video", "True"] }, then: true, else: false }
			},
			release_date: { $toDate: "$release_date" },
		},
	}]
);
print("Converting fields to corresponding type, Done !")

print("--- CREDITS ---")
convertAllStringToJSON(
	db.credits,
	"cast",
	"crew",
);