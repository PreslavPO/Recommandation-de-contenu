const { setCharAt, secondsToString } = require('./utils');
const axios = require('axios').default;

// Set up environment variable
require("dotenv").config({ path:__dirname+"/../.env" });

let totalSize = db.movies.aggregate([
	{ $match: { id: { $type: "int" } } },
	{ $count: "count" },
]).next().count;
let showEach = Math.floor(totalSize / 100);

let bulkOperations = [];
let counter = 0;
let startTime = new Date();
let endTime;

let errorDoc = [];

// Variables for the progress bar
let progressBar = "|" + "░".repeat(~~(totalSize/showEach)) + "|"
let counterBar = 0;
let progressCounter = -1;

// Remove cursor on the console
process.stdout.write("\x1B[?25l");

print("--- MOVIES ---")
process.stdout.clearLine(1);
process.stdout.cursorTo(0);
process.stdout.write(`Updating : ${progressBar} ${counter} / ${totalSize} !`)
process.stdout.write("\x1B[?25h"); // Put back the cursor on the console

db.movies.find({ id: { $type: "int" } }).forEach(async (doc) => {
	try {
		const res = await axios.get(`https://api.themoviedb.org/3/movie/${doc.id}?api_key=${process.env.TMDB_API_KEY}`);
		const data = res.data;
		bulkOperations.push({
			"updateOne": {
				"filter": { "_id": doc._id },
				"update": { "$set": {
					"poster_path": data.poster_path,
					"backdrop_path": data.backdrop_path,
				}}
			}
		});
	}
	catch (error) {
		if (error.response) {
			errorDoc.push(doc._id);
		}
		else if (error.request) {
			console.error("\n" + error.request);
		}
		else {
			console.error("\n" + error.message);
		}
	}
	counter++;

	// Make operations every certains amount of time
	if (counter % showEach == 0 && bulkOperations.length > 0) {
		db.movies.bulkWrite(bulkOperations, { w: 1 });
		bulkOperations = [];

		// Change progress bar variables
		progressCounter++;
		progressBar = setCharAt(progressBar, progressCounter+1, "▓");
		counterBar = counter;
	}

	// Time elapsed since beginning of the forEach
	endTime = new Date();
	let totalSeconds = Math.round((endTime - startTime) / 1000);

	// Print the progress of the process
	process.stdout.clearLine(1);
	process.stdout.cursorTo(0);
	process.stdout.write(`Updating : ${progressBar} ${counterBar} / ${totalSize} | Time elapsed : ${secondsToString(totalSeconds)}`);
});

// Traite les données qui restent
if (counter % showEach == 0 && bulkOperations.length > 0)
	db.movies.bulkWrite(bulkOperations, { w: 1 });

// Print done process
process.stdout.clearLine(0);
process.stdout.cursorTo(0);
process.stdout.write(`Updating : ${progressBar} ${counter} / ${totalSize} | Done !\n`)
process.stdout.write("\x1B[?25h"); // Put back the cursor on the console

print(errorDoc)