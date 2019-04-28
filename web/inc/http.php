<?php
class http_helper {
    private $limit = 100;
    private $skimmer = true;
    private $band;
    private $mode;
    private $source = 0;
    
    public function __construct(array $GETPARAMS = array(), array $POSTPARAMS = array()) {
        $this->limit = (int)($GETPARAMS["limit"]);
        $this->band = (int)($GETPARAMS["band"]);
        if (($GETPARAMS)["skimmer"] === 'false')
        {
            $this->skimmer = false;
        }
        else {
            $this->skimmer = (bool)$GETPARAMS["skimmer"];
        }
        $this->band = (string)$GETPARAMS["band"];
        $this->mode = (string)$GETPARAMS["mode"];
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

    public function get_skimmer(): bool
    {
        return($this->skimmer);
    }
    public function get_source(): int
    {
        return($this->source);
    }

}


?>