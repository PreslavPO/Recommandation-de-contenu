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

// Variables for the progress bar
let progressBar = "|" + "░".repeat(~~(totalSize/showEach)) + "|"
let progressCounter = 0;

// Remove cursor on the console
process.stdout.write("\x1B[?25l");

print("--- MOVIES ---")
process.stdout.clearLine(0);
process.stdout.cursorTo(0);
process.stdout.write(`Updating : ${progressBar} ${counter} / ${totalSize} !\n`)
process.stdout.write("\x1B[?25h"); // Put back the cursor on the console

db.movies.find({ id: { $type: "int" } }).forEach(async (doc) => {
	try {
		const res = await axios.get(`https://api.themoviedb.org/3/movie/${doc.id}?api_key=${process.env.TMDB_API_KEY}`);
		const data = res.data;

		bulkOperations.push({
			"updateOne": {
				"filter": { "_id": doc._id },
				"update": { "$set": {
					"poster_path": data.poster_path
				}}
			}
		});
		counter++;
	}
	catch (error) {
		console.error(error);
	}

	if (counter % showEach == 0) {
		db.movies.bulkWrite(bulkOperations, { w: 1 });
		bulkOperations = [];

		// Time elapsed since beginning of the forEach
		endTime = new Date();
		let totalSeconds = Math.round((endTime - startTime) / 1000);

		// Print the progress of the process
		process.stdout.clearLine(1);
		process.stdout.cursorTo(0);
		progressBar = setCharAt(progressBar, progressCounter+1, "▓");
		progressCounter++;
		process.stdout.write(`Updating : ${progressBar} ${counter} / ${totalSize} | Time elapsed : ${secondsToString(totalSeconds)}`);
	}
});

// Traite les données qui restent
if (counter % showEach == 0)
	db.movies.bulkWrite(bulkOperations, { w: 1 });

process.stdout.clearLine(0);
process.stdout.cursorTo(0);
process.stdout.write(`Converting string to object : ${progressBar} ${counter} / ${totalSize} | Done !\n`)
process.stdout.write("\x1B[?25h"); // Put back the cursor on the console