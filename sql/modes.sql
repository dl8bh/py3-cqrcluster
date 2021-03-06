DROP TABLE IF EXISTS `modes`;
CREATE TABLE `modes` (
  `mode_id` int(10) UNSIGNED NOT NULL,
  `mode_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `modes` VALUES(3, 'AM');
INSERT INTO `modes` VALUES(23, 'AMTOR');
INSERT INTO `modes` VALUES(9, 'ATV');
INSERT INTO `modes` VALUES(18, 'BPSK31');
INSERT INTO `modes` VALUES(25, 'BPSK63');
INSERT INTO `modes` VALUES(10, 'CLOVER');
INSERT INTO `modes` VALUES(1, 'CW');
INSERT INTO `modes` VALUES(17, 'CWQ');
INSERT INTO `modes` VALUES(46, 'DIGITALVOICE');
INSERT INTO `modes` VALUES(4, 'FM');
INSERT INTO `modes` VALUES(21, 'FSK44');
INSERT INTO `modes` VALUES(40, 'FSK441');
INSERT INTO `modes` VALUES(39, 'FT8');
INSERT INTO `modes` VALUES(11, 'GTOR');
INSERT INTO `modes` VALUES(14, 'HELL');
INSERT INTO `modes` VALUES(37, 'ISCAT');
INSERT INTO `modes` VALUES(29, 'JT4');
INSERT INTO `modes` VALUES(20, 'JT44');
INSERT INTO `modes` VALUES(31, 'JT65');
INSERT INTO `modes` VALUES(32, 'JT65A');
INSERT INTO `modes` VALUES(33, 'JT65B');
INSERT INTO `modes` VALUES(34, 'JT65C');
INSERT INTO `modes` VALUES(30, 'JT6M');
INSERT INTO `modes` VALUES(35, 'JT9');
INSERT INTO `modes` VALUES(19, 'MFSK');
INSERT INTO `modes` VALUES(28, 'MFSK16');
INSERT INTO `modes` VALUES(38, 'MSK144');
INSERT INTO `modes` VALUES(15, 'MT63');
INSERT INTO `modes` VALUES(12, 'MTOR');
INSERT INTO `modes` VALUES(27, 'OLIVIA');
INSERT INTO `modes` VALUES(26, 'PACKET');
INSERT INTO `modes` VALUES(7, 'PACTOR');
INSERT INTO `modes` VALUES(8, 'PSK');
INSERT INTO `modes` VALUES(41, 'PSK125');
INSERT INTO `modes` VALUES(44, 'PSK250');
INSERT INTO `modes` VALUES(13, 'PSK31');
INSERT INTO `modes` VALUES(42, 'PSK63');
INSERT INTO `modes` VALUES(36, 'QRA64');
INSERT INTO `modes` VALUES(16, 'QRSS');
INSERT INTO `modes` VALUES(45, 'ROS');
INSERT INTO `modes` VALUES(5, 'RTTY');
INSERT INTO `modes` VALUES(2, 'SSB');
INSERT INTO `modes` VALUES(6, 'SSTV');
INSERT INTO `modes` VALUES(24, 'THROB');
INSERT INTO `modes` VALUES(22, 'WSJT');
INSERT INTO `modes` VALUES(43, 'WSPR');


ALTER TABLE `modes`
  ADD PRIMARY KEY (`mode_id`),
  ADD KEY `mode_name` (`mode_name`);


ALTER TABLE `modes`
  MODIFY `mode_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;