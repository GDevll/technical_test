--Create schema
CREATE SCHEMA IF NOT EXISTS `phonedata`;

--Create tables
CREATE TABLE IF NOT EXISTS `phonedata`.`subscriber`(
    `invoice_acc`   INT NOT NULL,
    `invoice`       INT NOT NULL,
    `subscriber`    INT NOT NULL,
    PRIMARY KEY (`subscriber`)
);

CREATE TABLE IF NOT EXISTS `phonedata`.`msg`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `subscriber` INT NOT NULL,
    `date` DATE,
    `time` TIME,
    PRIMARY KEY (`id`),
    FOREIGN KEY(`subscriber`) REFERENCES `phonedata`.`subscriber`(`subscriber`)
);

CREATE TABLE IF NOT EXISTS `phonedata`.`call`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `subscriber`INT NOT NULL,
    `date` DATE,
    `time` TIME,
    `duration` TIME,
    `billed_duration` TIME NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY(`subscriber`) REFERENCES `phonedata`.`subscriber`(`subscriber`)
);

CREATE TABLE IF NOT EXISTS `phonedata`.`Iconnection`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `subscriber`INT NOT NULL,
    `date` DATE,
    `time` TIME,
    `amount` FLOAT NOT NULL,
    `billed_amount` FLOAT NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY(`subscriber`) REFERENCES `phonedata`.`subscriber`(`subscriber`)
);