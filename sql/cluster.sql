CREATE TABLE `cluster` (
  `de_call` varchar(20) NOT NULL,
  `qrg` float UNSIGNED DEFAULT NULL,
  `band_id` tinyint(3) UNSIGNED DEFAULT NULL,
  `dx_call` varchar(20) DEFAULT NULL,
  `mode_id` tinyint(3) UNSIGNED DEFAULT NULL,
  `comment` varchar(30) DEFAULT NULL,
  `speed` tinyint(4) DEFAULT NULL,
  `db` tinyint(4) DEFAULT NULL,
  `adif` smallint(5) UNSIGNED DEFAULT NULL,
  `sys_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `clx_timestamp` time DEFAULT NULL,
  `source` tinyint(4) NOT NULL,
  `skimmer` tinyint(1) NOT NULL,
  `id` bigint(20) UNSIGNED NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


ALTER TABLE `cluster`
  ADD PRIMARY KEY (`id`),
  ADD KEY `source` (`source`),
  ADD KEY `datetime` (`sys_datetime`),
  ADD KEY `dx_call` (`dx_call`),
  ADD KEY `de_call` (`de_call`),
  ADD KEY `band_id` (`band_id`),
  ADD KEY `mode_id` (`mode_id`),
  ADD KEY `adif` (`adif`),
  ADD KEY `skimmer` (`skimmer`);


ALTER TABLE `cluster`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;