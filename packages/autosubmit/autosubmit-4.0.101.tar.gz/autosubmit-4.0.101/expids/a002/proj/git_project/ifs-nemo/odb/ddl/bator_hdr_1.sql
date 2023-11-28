CREATE VIEW bator_hdr_1 AS
SELECT "*@sat","*@satob"
FROM  hdr,sat,satob
WHERE obstype = $satob
