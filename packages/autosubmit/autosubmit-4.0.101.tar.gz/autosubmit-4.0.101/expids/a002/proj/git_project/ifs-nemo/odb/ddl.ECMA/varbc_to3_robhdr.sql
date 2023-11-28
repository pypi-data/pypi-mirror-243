//
//-- ODB/SQL file 'varbc_to3_robhdr.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_to3_robhdr AS
  SELECT seqno,    
	 product_type@resat,
         body.len, 
         satellite_identifier@sat,
         sensor,   
  FROM   index, hdr, sat, resat
  WHERE  codetype = $resat
;
