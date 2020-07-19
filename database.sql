--Create schema
CREATE SCHEMA IF NOT EXISTS `phonedata`;

--Create tables

-- Table of subscribers
CREATE TABLE IF NOT EXISTS `phonedata`.`subscriber`(
    `invoice_acc`   INT NOT NULL,
    `invoice`       INT NOT NULL,
    `subscriber`    INT NOT NULL,
    PRIMARY KEY (`subscriber`)
);

-- Table of messages
CREATE TABLE IF NOT EXISTS `phonedata`.`msg`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `subscriber` INT NOT NULL,
    `date` DATE NOT NULL,
    `time` TIME NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY(`subscriber`) REFERENCES `phonedata`.`subscriber`(`subscriber`)
);

--Table of calls
CREATE TABLE IF NOT EXISTS `phonedata`.`call`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `subscriber`INT NOT NULL,
    `date` DATE NOT NULL,
    `time` TIME NOT NULL,
    `duration` TIME NOT NULL,
    `billed_duration` TIME NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY(`subscriber`) REFERENCES `phonedata`.`subscriber`(`subscriber`)
);

-- Table of cellular connection
CREATE TABLE IF NOT EXISTS `phonedata`.`Iconnection`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `subscriber`INT NOT NULL,
    `date` DATE NOT NULL,
    `time` TIME NOT NULL,
    `amount` FLOAT NOT NULL,
    `billed_amount` FLOAT NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY(`subscriber`) REFERENCES `phonedata`.`subscriber`(`subscriber`)
);