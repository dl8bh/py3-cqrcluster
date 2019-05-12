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
        $this->sources = $this::get_sources();
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
    public function get_sources(): array
    {
        $this->dbconnect->select_db("cqrlog_common");
        $result = mysqli_query($this->dbconnect, "SELECT * from dxclusters ORDER BY id_dxclusters");
        $dxclusters = array();
        while ($row = mysqli_fetch_object($result))
        {
            $dxclusters[$row->id_dxclusters] = $row->description;
        }
        return $dxclusters;
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

    public function get_last_n_lines(int $count = 0, int $band = 0, int $mode = 0, int $skimmer = 1, int $adif = 0, int $source = int) :array 
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
        if ($band != 0)
        {
            $where .= " AND band_id = '" . $band . "'";
        }
        if ($adif != 0)
        {
            $where .= " AND adif = '" . $adif . "'";
        }
        if ($source != 0)
        {
            $where .= " AND source = '" . $source . "'";
        }
        if ($skimmer === 0) // cluster only
        {
            $where .= " AND skimmer = 0";
        }
        else if ($skimmer === 1) assert(true); // both skimmer and cluster
        else if ($skimmer === 2) // skimmer only
        {  
            $where .= " AND skimmer = 1";
        }
        $query .= $where . " ORDER BY id DESC LIMIT " . $count;
        $result = mysqli_query($this->dbconnect, $query);
        while ($row = mysqli_fetch_object($result))
        {
            $line = array();
            $line["DE_CALL"] = $row->de_call;
            $line["QRG"] = $row->qrg;
            $line["BAND"] = $this->bands[$row->band_id]["NAME"];
            $line["MODE"] = $this->modes[$row->mode_id];
            $line["DX_CALL"] = $row->dx_call;
            $line["ADIF"] = $row->adif;
            $line["COMMENT"] = $row->comment;
            $line["SPEED"] = $row->speed;
            $line["DB"] = $row->db;
            $line["SYS_DATETIME"] = $row->sys_datetime;
            $line["timestamp"] = $row->clx_timestamp;
            $line["source"] = $row->source;
            $line["skimmer"] = $row->skimmer;
            $line["ID"] = $row->id;
            array_push($lines, $line);
        }
        return $lines;
    }

    public function id_to_band(int $id): string
    {   
        foreach ($this->bands as $band_id => $band_details)
        {
            if ($id == $band_id) return $band_details["NAME"];
        }
        return '';
    }

    public function band_to_id( string $band): int
    {   
        foreach ($this->bands as $band_id => $band_details)
        {
            if ($band_details["NAME"] == strtoupper($band)) return $band_id;
        }
        return 0;
    }

    public function mode_to_id( string $mode): int
    {   
        foreach ($this->modes as $mode_id => $mode_name)
        {
            if ($mode_name == strtoupper($mode)) return $mode_id;
        }
        return 0;
    }
    public function id_to_source (int $id): string
    {   
        foreach ($this->sources as $source_id => $source_name)
        {
            if ($id == $source_id) return $source_name;
        }
        return '';
    }
    public function source_to_id( string $source): int
    {   
        foreach ($this->sources as $source_id => $source_name)
        {
            if ($source_name == strtoupper($source)) return $source_id;
        }
        return 0;
    }
}


?>