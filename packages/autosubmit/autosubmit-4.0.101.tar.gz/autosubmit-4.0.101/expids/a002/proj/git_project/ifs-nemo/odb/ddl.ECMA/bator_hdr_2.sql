CREATE VIEW bator_hdr_2 AS
SELECT "*@sat","*@radiance"
FROM  hdr,sat,radiance
WHERE obstype = $satem AND codetype = $atovs
