CREATE VIEW small AS
SELECT
   lat, lon, trlat, trlon, obstype 
FROM  index, hdr
