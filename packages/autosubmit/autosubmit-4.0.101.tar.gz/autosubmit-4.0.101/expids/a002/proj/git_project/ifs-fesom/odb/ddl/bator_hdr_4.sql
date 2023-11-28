CREATE VIEW bator_hdr_4 AS
SELECT "*@sat","*@radiance","*@ssmi"
FROM  hdr,sat,radiance,ssmi
WHERE obstype = $satem AND codetype = $ssmi 
