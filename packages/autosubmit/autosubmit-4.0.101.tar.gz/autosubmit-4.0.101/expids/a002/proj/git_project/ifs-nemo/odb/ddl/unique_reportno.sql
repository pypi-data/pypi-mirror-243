
READONLY;

CREATE VIEW unique_reportno AS
SELECT seqno,
       reportno UPDATED,
       statid,
       reportype // to distinguish duplicate reports with the same statid (e.g. BUFR vs. TAC).
FROM hdr;

