-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema userdashboard
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema userdashboard
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `userdashboard` DEFAULT CHARACTER SET utf8 ;
USE `userdashboard` ;

-- -----------------------------------------------------
-- Table `userdashboard`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `userdashboard`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `pw_hash` VARCHAR(255) NULL,
  `description` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_level` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `userdashboard`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `userdashboard`.`messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `message` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  `wall_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_messages_users_idx` (`user_id` ASC),
  CONSTRAINT `fk_messages_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `userdashboard`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `userdashboard`.`comments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `userdashboard`.`comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `comment` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `message_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comments_messages1_idx` (`message_id` ASC),
  INDEX `fk_comments_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_comments_messages1`
    FOREIGN KEY (`message_id`)
    REFERENCES `userdashboard`.`messages` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comments_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `userdashboard`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
