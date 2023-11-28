// Anne Fouilloux - Add sat table. I know this is not what you want...
// need to discuss with Dominique...

READONLY;

SET $tslot = -1;

CREATE VIEW manda_gene_hdr AS
SELECT body.len, procid, obstype, codetype, report_status@hdr, satellite_identifier@sat, sensor
FROM  index, hdr,sat 
WHERE timeslot = $tslot
