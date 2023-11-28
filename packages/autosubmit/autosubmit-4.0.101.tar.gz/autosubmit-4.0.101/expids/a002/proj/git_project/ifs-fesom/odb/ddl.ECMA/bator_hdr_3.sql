CREATE VIEW bator_hdr_3 AS
SELECT "*@sat","*@scatt"
FROM  hdr,sat,scatt
WHERE obstype = $scatt
