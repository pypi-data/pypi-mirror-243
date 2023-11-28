CREATE VIEW bator_hdr_6 AS
SELECT "*@sat","*@gnssro"
FROM  hdr,sat,gnssro
WHERE codetype = $gpsro
