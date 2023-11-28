READONLY;

CREATE VIEW fcq_robhdr_1 AS
SELECT  
   body.len,
   obstype, sitedep, bufrtype, stalt,              //  tables hdr integer
   codetype, date, time, lat, lon, statid         //  table hdr
FROM  index, hdr
WHERE  (obstype = $synop)
 AND   ((codetype = 11) OR (codetype = 14))
