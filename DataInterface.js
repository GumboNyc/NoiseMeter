//const SQLiteTagSpawned = require('sqlite-tag-spawned');
//const {query, get, all, raw, transaction} = SQLiteTagSpawned('./Database/NoiseRecords.db');

var dblite = require('dblite'),
db = dblite( __dirname + '/Database/NoiseRecords.db');

module.exports = {
    VolumesBetweenDates: function (startDate, endDate, callback) {
      if(isNaN(startDate) || isNaN(endDate)){
        startDate = Date.now() - 60*60*1000;
        endDate = Date.now();
      }

      db.query(`SELECT * FROM noise_records where record_time > ${startDate/1000}  and record_time < ${endDate/1000}`, function(err, rows) {
        callback(rows);
      });
    }};