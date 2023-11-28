//
//-- ODB/SQL file 'prtdpst_robody.sql'
//
//   Last updated:  10-Oct-2001
//

CREATE VIEW prtdpst_robody AS
  SELECT seqno, entryno, varno,
	 vertco_reference_1, vertco_reference_2, an_depar,  // body
	 hires                // update[1]
  FROM   index, hdr, body, update[1]
