<?php
class http_helper {
    private $limit = 100;
    private $skimmer = 1;
    private $band;
    private $mode;
    private $source = '';
    
    public function __construct(array $GETPARAMS = array(), array $POSTPARAMS = array()) {
        $this->limit = (int)($GETPARAMS["limit"]);
        $this->band = (int)($GETPARAMS["band"]);
        if (!isset($GETPARAMS["skimmer"]))
        {
            $this->skimmer = 1;
        }
        else {
            $this->skimmer = (int)$GETPARAMS["skimmer"];
        }
        $this->band = (string)$GETPARAMS["band"];
        $this->mode = (string)$GETPARAMS["mode"];
        $this->source = (string)$GETPARAMS["source"];
        if ((int)$GETPARAMS["limit"]) {
            $this->limit = (int)$GETPARAMS["limit"];
        }

        
    }
    
    public function get_limit(): int
    {
        return($this->limit);
    }
    
    public function get_band(): string
    {
        return($this->band);
    }

    public function get_mode(): string
    {
        return($this->mode);
    }

    public function get_skimmer(): int
    {
        return($this->skimmer);
    }
    public function get_source(): string
    {
        return($this->source);
    }

}


?>