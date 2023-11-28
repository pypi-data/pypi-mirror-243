// psbias_compress_method_1a

SET $basedate = -1;
SET $basetime = -1;
SET $no_of_days_ago = -1;

SET $all = 0;

CREATE VIEW psbias_compress_method_1a AS
SELECT body FROM hdr // gets body.offset & body.len, in this order
 WHERE ($all == 1) OR (
       date is not null
   AND time is not null
   AND date < $basedate
   AND ABS(tdiff(date,time,$basedate,$basetime)) > $no_of_days_ago * 24 * 3600
                      )
ORDER BY 1 // Sort w.r.t. body.offset in ODB_get()
;
