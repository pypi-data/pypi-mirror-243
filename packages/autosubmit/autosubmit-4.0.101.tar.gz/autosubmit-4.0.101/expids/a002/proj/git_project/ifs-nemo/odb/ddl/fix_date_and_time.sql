// To fetch incorrect times (seconds at 60) for fixing

UPDATED; // Note : NOT Read/Only !!

CREATE VIEW fix_date_and_time AS
  SELECT date, time
    FROM hdr
   WHERE mod(time,100) = 60
;
