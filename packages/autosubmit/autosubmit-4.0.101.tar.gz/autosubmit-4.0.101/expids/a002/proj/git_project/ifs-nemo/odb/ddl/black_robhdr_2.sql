//
//   Blacklisting default header query + sat default + satob
//
//   == ALWAYS keep black*1.sql to black*10.sql consistent! ==
//

READONLY; // Except entries those marked with  UPDATED

SET $kset = 0;
SET $tslot = -1;

CREATE VIEW black_robhdr_2 AS
  SELECT seqno, // BLACKLIST CORE HDR START. SEQNO MUST COME FIRST
         abnob,
         mapomm,
         body.len,
         obstype,
         codetype,
         instrument_type@hdr,
         retrtype,
         areatype,
         date,
         time,
         report_status  UPDATED,
         report_blacklist  UPDATED,
         stalt,
         lat,
         lon,
         orography,
         statid,
         reportype,
         source,
         sensor, // BLACKLIST CORE HDR END
         satellite_identifier@sat, // SAT CORE HDR START
         zenith@sat,
         azimuth@sat,
         gen_centre@sat,
         gen_subcentre@sat,
         datastream@sat,
         solar_zenith@sat, // SAT CORE HDR END
         comp_method@satob,
         QI_fc@satob,
         RFF@satob,
         QI_nofc@satob,
  FROM   timeslot_index, index, hdr, modsurf, sat, satob
  WHERE (obstype = $satob)
    AND  (kset = $kset)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
