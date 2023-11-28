READONLY;

SET $angle_min = -1;
SET $angle_max = -1;
SET $polarisation = -1;

CREATE VIEW averaging_smos
  SELECT  seqno,
          entryno,
          lat,
          lon,
          date,
          time,
          obsvalue UPDATED,
          incidence_angle UPDATED,
          nobs_averaged UPDATED,
          stdev_averaged UPDATED,
          report_status UPDATED,
          datum_status UPDATED,
          rad_acc_pure UPDATED,
          faradey_rot_angle UPDATED,
          pixel_rot_angle UPDATED,
FROM hdr,body,smos
WHERE $angle_min <= incidence_angle <= $angle_max
AND polarisation=$polarisation
ORDER BY lat,lon, date, time

