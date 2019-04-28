<?php
class cqrdb {
    private $db_hostname;
    private $db_username;
    private $db_password;
    private $db;
    private $dbconnect;
    private $bands;
    private $modes;
    private $defaultcount = 100;

    public function __construct($db_hostname, $db_username, $db_password, $db) {
        $this->db_hostname = $db_hostname;
        $this->db_username = $db_username;
        $this->db_password = $db_password;
        $this->db = $db;
        $this->dbconnect = mysqli_connect($db_hostname, $db_username, $db_password, $db);
        if(!$this->dbconnect) {
            exit("Database connection failure: ".mysqli_connect_error());
        }
        $this->bands = $this::get_bands();
        $this->modes = $this::get_modes();
    }
    
    public function set_default_count(int $count)
    {
        $this->defaultcount = $count;
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
            $band["F_SSB"] = $row->ssb;
            $band["F_RTTY"] = $row->rtty;
            $bands[$band["ID"]] = $band;
        }
        return $bands;
    }

    public function get_modes(): array
    {
        $this->dbconnect->select_db("cqrlog_common");
        $result = mysqli_query($this->dbconnect, "SELECT * from modes ORDER BY mode_id");
        while ($row = mysqli_fetch_object($result))
        {
            $mode = array();
            $mode["ID"] = $row->mode_id;
            $mode["NAME"] = $row->mode_name;
            $modes[$mode["ID"]] = $mode["NAME"];
        }
        return $modes;
    }

    public function get_last_n_lines(int $count = 0, int $band = 0, int $mode = 0, int $source = int) :array 
    {   
        $this->dbconnect->select_db("cqrlog_common");
        $lines = array();
        $query = "SELECT * from cluster";
        $where = " WHERE 1 = 1";
        if ($count == 0)
        {
            $count = $this->defaultcount;
        }
        if ($mode != 0)
        {
            $where .= " AND mode_id = '" . $mode . "'";
        }
        echo $where;
        $query .= $where . " ORDER BY id DESC LIMIT " . $count;
        echo $query;
        $result = mysqli_query($this->dbconnect, $query);
        while ($row = mysqli_fetch_object($result))
        {
            $line = array();
            $line["DE_CALL"] = $row->de_call;
            $line["QRG"] = $row->qrg;
            $line["BAND"] = $this->bands[$row->band_id]["NAME"];
            $line["MODE"] = $this->modes[$row->mode_id];
            $line["COMMENT"] = $row->comment;
            $line["SPEED"] = $row->speed;
            $line["DB"] = $row->db;
            $line["SYS_DATETIME"] = $row->sys_datetime;
            $line["timestamp"] = $row->clx_timestamp;
            $line["source"] = $row->source;
            $line["ID"] = $row->id;
            array_push($lines, $line);
        }
        return $lines;
    }

}


?>