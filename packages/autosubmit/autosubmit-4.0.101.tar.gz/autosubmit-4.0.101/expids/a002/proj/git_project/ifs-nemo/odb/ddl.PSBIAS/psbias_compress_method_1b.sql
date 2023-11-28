// psbias_compress_method_1b

SET $body_min = -1;
SET $body_chunk = -1;

CREATE VIEW psbias_compress_method_1b AS
// Apply this only AFTER links have been massaged
SELECT "*@body" FROM hdr,body
 WHERE ($body_min <= #body < $body_min + $body_chunk)
;
