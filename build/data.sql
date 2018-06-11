SET FOREIGN_KEY_CHECKS = 0;


INSERT INTO `api_course` (`id`, `name`, `description`, `user_id`, `image`, `subscribers`, `native_lang_id`, `trans_lang_id`, `public`) VALUES
(1, 'Peninsular Spanish for beginners', 'This course is meant for those who are interested in learning Spanish the way it is spoken in Spain.', 0, 'http://wallpoper.com/images/00/38/97/83/cityscapes-spain_00389783.jpg', 1, 1, 6, 1);

INSERT INTO `api_language` (`id`, `name`, `flag`) VALUES
(1, 'English', 'england'),
(2, 'Dutch', 'netherlands'),
(3, 'German', 'germany'),
(4, 'French', 'france'),
(5, 'Russian', 'russia'),
(6, 'Spanish', 'spain');

INSERT INTO `api_lesson` (`id`, `name`, `category`, `description`, `course_id`) VALUES
(1, 'Welcome to Spain', 'basic phrases', 'A quick introduction to the Spanish language.', 'Grammar here.', 1);

INSERT INTO `api_lessontype` (`id`, `name`, `description`) VALUES
(1, 'Grammar', 'Learn grammar'),
(2, 'Flashcards', 'Learn with flashcards'),
(3, 'Completion', 'Learn with completion exercises');

INSERT INTO `api_subscription` (`id`, `course_id`, `user_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 1, 3),
(4, 3, 1),
(5, 2, 3),
(6, 3, 2);

INSERT INTO `api_favorite` (`id`, `course_id`, `user_id`) VALUES
(1,1,1),
(2,2,1),
(3,1,3),
(4,3,1);

INSERT INTO `api_user` (`id`, `email`, `name`, `password`, `distributor`,`attempt`) VALUES
(1, 'piet@hotmail.com', 'piet', 'welkom123', 0,0),
(2, 'jan@hotmail.com', 'jan', 'welkom123', 1,0),
(3, 'peter@hotmail.com', 'peter', 'welkom123', 0,0),
(4, 'sara@hotmail.com', 'sara', 'welkom123', 1,0),
(5, 'evert@hotmail.com', 'evert', 'welkom123', 0,0);


INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$100000$kEJf41igeCuu$iHOT0wafWzt+SlSOD7N7iPdigUNx5bzVJfz5g8JPyR8=', '2018-05-30 08:00:26.447438', 1, 'root', '', '', 'bertde.boer@hotmail.com', 1, 1, '2018-05-30 07:59:58.949897');

INSERT INTO `api_wordlistquestion` (`id`, `native`, `translation`, `lesson_id`) VALUES
(1, 'Hello', 'Hola', 1),
(2, 'How are you? (informal)', '¿Qué tal?', 1),
(3, 'Spain', 'España', 1),
(4, 'I am twenty years old.', 'Tengo veinte años.', 1),
(5, 'Please', 'Por favor', 1),
(6, 'Thank you', 'Gracias', 1),
(7, 'Thank you very much', 'Muchas gracias', 1),
(8, 'Help me!', 'Ayúdame!', 1),
(9, 'A beer, please.', 'Una cerveza, por favor.', 1),
(10, 'Is there a supermarket nearby?', 'Hay un supermercado por aquí cerca?', 1);

SET FOREIGN_KEY_CHECKS = 1;