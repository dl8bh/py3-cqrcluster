<?php
class cqrdb {
    private $db_hostname;
    private $db_username;
    private $db_password;
    private $db;
    private $dbconnect;
    private $bands;

    public function __construct($db_hostname, $db_username, $db_password, $db) {
        $this->db_hostname = $db_hostname;
        $this->db_username = $db_username;
        $this->db_password = $db_password;
        $this->db = $db;
        $this->dbconnect = mysqli_connect($db_hostname, $db_username, $db_password, $db);
        if(!$this->dbconnect) {
            exit("Database connection failure: ".mysqli_connect_error());
        }
    }
    
    public function get_bands(): array
    {
        $this->dbconnect->select_db("cqrlog_common");
        $result = mysqli_query($this->dbconnect, "SELECT * from bands ORDER BY b_begin asc");
        $bands = array();
        while ($row = mysqli_fetch_object($result))
        {
            $band = array();
            $band["ID"] = $row->id_bands;
            $band["NAME"] = $row->band;
            $band["F_BEGIN"] = $row->b_begin;
            $band["F_END"] = $row->b_end;
            $band["F_CW"] = $row->cw;
            $band["F_SSB"] = $row->SSB;
            $band["F_RTTY"] = $row->RTTY;
            $bands[$band["ID"]] = $band;
        }
        return $bands;
    }

    public function get_last_n_lines(int $count = 0, int $band = 0, int $mode = 0, array $source = array()) :array 
    {
        return array();
    }

}


?>