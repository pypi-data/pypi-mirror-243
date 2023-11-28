// psbias_compress_method_0

SET $basedate = -1;
SET $basetime = -1;
SET $no_of_days_ago = -1;

SET $body_min = -1;
SET $body_chunk = -1;

CREATE VIEW psbias_compress_method_0 AS
SELECT "*@body" FROM hdr,body
 WHERE date is not null
   AND time is not null
   AND date < $basedate
   AND ABS(tdiff(date,time,$basedate,$basetime)) > $no_of_days_ago * 24 * 3600
   AND (
    ($body_min == -1) OR 
    ($body_chunk == -1) OR 
    ($body_min <= #body < $body_min + $body_chunk)
       )
;
