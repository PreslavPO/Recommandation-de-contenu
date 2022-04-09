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
 * Convert seconds to a formated string
 * @param {int} totalSeconds seconds that will be converted
 * @returns String in the format minutes:seconds (e.g. 12:55)
 */
const secondsToString = (totalSeconds) => {
	const minutes = ~~(totalSeconds / 60); //~~ <=> Math.floor
	const seconds = ~~totalSeconds % 60;
	return ((minutes > 0) ? minutes + ":" : "") + ((minutes >= 1 && seconds < 10) ? "0" : "") + seconds;
}

module.exports = {
	setCharAt,
	secondsToString,
}