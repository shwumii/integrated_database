--DROP DATABASE `ghibli`;
CREATE DATABASE `ghibli`;

USE `ghibli`;

CREATE TABLE IF NOT EXISTS `movie` (
  `movieID` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `releaseYear` int NOT NULL,
  `director` varchar(50) NOT NULL,
  `length` int NOT NULL,
  `rating` varchar(10) NOT NULL DEFAULT 'PG',
  PRIMARY KEY (`movieID`)
);

INSERT INTO `movie` (`movieID`, `title`, `releaseYear`, `director`, `length`, `rating`) VALUES 
(1, 'Nausicaa of the Valley of the Wind', 1984, 'Hayao Miyazaki', 116, 'PG'),
(2, 'Castle in the Sky', 1986, 'Hayao Miyazaki', 124, 'PG'),
(3, 'Grave of the Fireflies',1988,'Isao Takahata',88,'NR'),
(4, 'My Neighbour Totoro',1988,'Hayao Miyazaki',86,'G'),
(5, 'Kikis Delivery Service',1989,'Hayao Miyazaki',103,'G'),
(6, 'Only Yesterday',1991,'Isao Takahata',119,'PG'),
(7, 'Porco Rosso',1992,'Hayao Miyazaki',92,'PG'),
(8, 'Ocean Waves',1993,'Tomomi Mochizuki',72,'PG 13+'),
(9, 'Pom Poko',1994,'Isao Takahata',119,'PG'),
(10, 'Whisper of the Heart',1995,'Yoshifumi Kondo',111,'G'),
(11, 'Princess Mononoke',1997,'Hayao Miyazaki',133,'PG 13+'),
(12, 'My Neighbours the Yamadas',1999,'Isao Takahata',103,'PG'),
(13, 'Spirited Away',2001,'Hayao Miyazaki',124,'PG'),
(14, 'The Cat Returns',2002,'Hiroyuki Morita',75,'G'),
(15, 'Howls Moving Castle',2004,'Hayao Miyazaki',119,'PG'),
(16, 'Tales from Earthsea',2006,'Goro Miyazaki',115,'PG 13+'),
(17, 'Ponyo',2008,'Hayao Miyazaki',103,'G'),
(18, 'The Secret World of Arrietty',2010,'Hiromasa Yonebayashi',95,'G'),
(19, 'From Up on Poppy Hill',2011,'Goro Miyazaki',92,'PG'),
(20, 'The Wind Rises',2013,'Hayao Miyazaki',127,'PG 13+'),
(21, 'The Tale of the Princess Kaguya',2013,'Isao Takahata',137,'PG'),
(22, 'When Marnie Was There',2014,'Hiromasa Yonebayashi',102,'PG'),
(23, 'Earwig and the Witch',2020,'Goro Miyazaki',82,'PG'),
(24, 'The Boy and the Heron',2023,'Hayao Miyazaki',125,'PG');

CREATE TABLE IF NOT EXISTS `member` (
  `memberID` int NOT NULL AUTO_INCREMENT,
  `member_name` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `usrid` varchar(12) NOT NULL,
  `usrpwd` varchar(12) NOT NULL,
  PRIMARY KEY (`memberID`)
);

INSERT INTO `member` (`memberID`, `member_name`, `email`, `usrid`, `usrpwd`) VALUES 
(1, 'Hans Telford', 'hans@geemail.com', 'hans123', 'hans123'),
(2, 'Marty McFly', 'marty@geemail.com', 'marty123', 'marty123'),
(3, 'Jimmy Page', 'jimmy@geemail.com', 'jimmy123', 'jimmy123'),
(4, 'Will Stanford', 'will.stanford@xyz.com.au', 'will123', 'will123'),
(5, 'Michael Pandora', 'michael.pandora@xyz.com.au', 'michael123', 'michael123'),
(6, 'Sally Goswell', 'sally.goswell@xyz.com.au', 'sally123', 'sally123');

CREATE TABLE IF NOT EXISTS `discussion` (
  `discussionID` int NOT NULL AUTO_INCREMENT,
  `memberID` int NOT NULL,
  `movieID` int NOT NULL,
  `commentDate` varchar(12),
  `comments` varchar(256) NOT NULL,
  PRIMARY KEY (`discussionID`),
  CONSTRAINT `fk_memberID` FOREIGN KEY (`memberID`) REFERENCES member(`memberID`),
  CONSTRAINT `fk_movieID` FOREIGN KEY (`movieID`) REFERENCES movie(`movieID`)
);

INSERT INTO `discussion` (`discussionID`, `memberID`, `movieID`, `commentDate`, `comments`) VALUES 
(1, 1, 11, '01-Oct-2024', 'A beautifully made pro-environment film by Hiyazaki - definitely a must see!'),
(2, 2, 11, '01-Oct-2024', 'One of Miyazakis best - the story and characters are amazing.'),
(3, 3, 13, '01-Oct-2024', 'Spirited Away won an academy award - see the film and you will know why. Its a masterpiece by Hiyazaki'),
(4, 4, 8, '01-Sep-2024', 'The title lends credence to the story as it refers to the idea that teenage feelings are like waves - ever changing.'),
(5, 5, 8, '01-Sep-2024', 'A delicate, well-told drama that may lack the depth of something like Only Yesterday.'),
(6, 6, 21, '02-Sep-2024', 'Great narrative depth, frank honesty and exquisite visual beauty.'),
(7, 4, 3, '03-Sep-2024', 'An achingly sad anti-war film, it is one of Studio Ghiblis most profoundly beautiful, haunting work.'),
(8, 5, 6, '04-Sep-2024', 'Emotionally honest film primarily aimed at female viewers.'),
(9, 6, 5, '05-Sep-2024', 'Heartwarming and gorgeously rendered tale of a young witch who discovers her place in the world.'),
(20, 3, 1, '02-Oct-2024', 'Nausicaa of the Valley of the Wind - A wonderfully told story of a young brave princess and her struggle against a warring humanity and the destruction of the environment.'),
(21, 3, 2, '02-Oct-2024', 'Castle in the Sky - really enjoyed the pirates in this - great story - one of Miyazakis best.'),
(22, 3, 3, '02-Oct-2024', 'Grave of the Fireflies - the saddest anime I have ever seen - made me very tearful.'),
(23, 4, 4, '03-Oct-2024', 'My Neighbor Totoro is a heartwarming, sentimental masterpiece that captures the simple grace of childhood.'),
(24, 4, 5, '03-Oct-2024', 'Emotionally honest film primarily aimed at female viewers.'),
(25, 4, 7, '03-Oct-2024', 'A marvellous tale of a flying ace who is cursed pig man and who battles air pirates.'),
(26, 6, 8, '03-Oct-2024', 'A delicate, well-told drama that may lack the depth of something like Only Yesterday.'),
(28, 6, 9, '03-Oct-2024', 'A wonderful story of shape-shifting raccoons band who together to save their forest homeland from the bulldozers of greedy land developers.'),
(29, 3, 11, '03-Oct-2024', 'With its epic story and breathtaking visuals, Princess Mononoke is a landmark in the world of animation.'),
(30, 1, 12, '03-Oct-2024', 'The adventures of a modern family in Japan'),
(31, 1, 13, '03-Oct-2024', 'Spirited Away is a dazzling, enchanting, and gorgeously drawn fairy tale that will leave viewers a little more curious and fascinated by the world around them.'),
(32, 1, 14, '03-Oct-2024', 'Sweetly charming and beautifully animated, this film offers anime adventure suitable for the very young and young at heart.'),
(33, 1, 15, '03-Oct-2024', 'Howls Moving Castle is exquisitely illustrated. This anime film will delight children with its fantastical story and touch the hearts and minds of older viewers as well.'),
(34, 1, 16, '03-Oct-2024', 'In the land of Earthsea, a mysterious force threatens to plunge humanity into destruction and chaos.'),
(35, 1, 17, '03-Oct-2024', 'While not Miyazakis best film, Ponyo is a visually stunning fairy tale thats a sweetly poetic treat for children of all ages.'),
(36, 1, 18, '03-Oct-2024', 'The Secret World of Arrietty - Visually lush, refreshingly free of family-friendly clatter, and anchored with soulful depth.'),
(37, 1, 19, '03-Oct-2024', 'Gentle and nostalgic, From Up on Poppy Hill is one of Studio Ghiblis sweeter efforts -- and if it does not push the boundaries of the genre, it remains as engagingly lovely as Ghibli fans have come to expect.'),
(38, 1, 20, '03-Oct-2024', 'Fittingly bittersweet and inspirational story of a Japanese aviation engineer.'),
(39, 1, 21, '03-Oct-2024', 'The Tale of the Princess Kaguya - Amazing story and beautifully animated in a traditional style.'),
(40, 1, 22, '03-Oct-2024', 'When Marnie Was There is still blessed with enough visual and narrative beauty to recommend, even if it is not quite as magical as Studio Ghiblis greatest works.'),
(41, 1, 23, '03-Oct-2024', 'With a story as uninspired as its animation, Earwig and the Witch is a surprising and near-total misfire for Studio Ghibli.'),
(42, 1, 24, '03-Oct-2024', 'The Boy and the Heron - this is a film with soulfully exploring thought-provoking themes through a beautifully animated lens.');
