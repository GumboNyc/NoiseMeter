//const SQLiteTagSpawned = require('sqlite-tag-spawned');
//const {query, get, all, raw, transaction} = SQLiteTagSpawned('./Database/NoiseRecords.db');

var dblite = require('dblite'),
db = dblite('./Database/NoiseRecords.db');

module.exports = {
    VolumesBetweenDates: function (startDate, endDate, callback) {
      db.query('SELECT * FROM noise_records where record_time > ' + (Date.now()/1000 - 60*60), function(err, rows) {
        callback(rows);
      });
      //return await get(`SELECT * FROM noise_records`);
    }};