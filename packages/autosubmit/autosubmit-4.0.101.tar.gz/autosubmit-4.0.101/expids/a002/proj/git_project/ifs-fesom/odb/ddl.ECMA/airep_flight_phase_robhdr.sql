//
//-- ODB/SQL file 'airep_flight_phase_robhdr.sql'
//
//   Last updated:  14-Mar-2018

//

READONLY;

CREATE VIEW airep_flight_phase_robhdr AS
     SELECT seqno,
            body.len,
            statid, obstype, codetype, date,
            time,
            lat, lon,
            flight_phase, 
            flight_dp_o_dt UPDATED,
            heading        UPDATED,
            varno, obsvalue,
            vertco_type,
            vertco_reference_1,
      FROM index, hdr, conv, body
      WHERE obstype==$airep and varno==2
      ORDERBY codetype, statid, date, time, vertco_reference_1
;
