CREATE VIEW cycle_biasprep_satpred AS
SELECT
   lsm,
   orography,
   snow_depth,
   t2m,
   albedo,
   windspeed10m,
   surface_class,
   skintemper,
   skintemp[1:($NMXUPD+1)],
   cldptop_3,
   cldne_3,
FROM  hdr, sat, modsurf, radiance, radiance
WHERE  (obstype = $satem)
 AND   (codetype = $atovs)
