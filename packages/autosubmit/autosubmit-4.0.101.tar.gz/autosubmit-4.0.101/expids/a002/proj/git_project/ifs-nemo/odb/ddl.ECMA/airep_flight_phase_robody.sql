//
//-- ODB/SQL file 'airep_flight_phase_robody.sql'
//
//   Last updated:  30-Jun-2005

//

READONLY;

CREATE VIEW airep_flight_phase_robody AS
     SELECT seqno,
            varno, obsvalue,
            vertco_type,
            vertco_reference_1,
      FROM  index, hdr, body
      WHERE obstype==$airep and varno==2
      ORDERBY codetype, statid, date, time, vertco_reference_1
;
