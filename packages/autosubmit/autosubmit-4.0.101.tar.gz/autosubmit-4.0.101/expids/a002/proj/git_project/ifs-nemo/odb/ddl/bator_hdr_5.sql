CREATE VIEW bator_hdr_5 AS
SELECT "*@sat","*@radar"
FROM  hdr,sat,radar
WHERE obstype = $radar
