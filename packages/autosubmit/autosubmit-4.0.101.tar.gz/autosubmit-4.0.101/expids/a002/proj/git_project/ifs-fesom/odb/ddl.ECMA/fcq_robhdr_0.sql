READONLY;

SET $obstype = 0;
SET $codetype = 0;

CREATE VIEW fcq_robhdr_0 AS
SELECT  
   body.len,
   obstype, sitedep, bufrtype, stalt,           //  tables hdr integer
   codetype, date, time, lat, lon, statid,       //  table hdr
   report_status,
FROM  index, hdr
WHERE  (obstype = $obstype) AND (codetype = $codetype)