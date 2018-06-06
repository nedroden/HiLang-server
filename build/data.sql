--
-- Database: `hilang`
--

SET FOREIGN_KEY_CHECKS = 0;

--
-- Gegevens worden geëxporteerd voor tabel `api_course`
--

INSERT INTO `api_course` (`id`, `name`, `description`, `language_id`, `user_id`, `image`, `subscribers`) VALUES
(1, 'English for beginners', 'Learn to write English properly.', 1, 1, 'http://www.linguapaths.com/wp-content/uploads/2016/09/regular-english-course-valencia.jpg', 69),
(2, 'French for beginners', 'Learn to speak French properly', 4, 4, 'https://i.pinimg.com/originals/3a/14/f0/3a14f0325f7316ef603539116dae02ac.jpg', 420),
(3, 'German for beginners', 'Learn to write Germam properly', 3, 4, 'https://www.imperial.ac.uk/ImageCropToolT4/imageTool/uploaded-images/deutsch-2--tojpeg_1437992131488_x2.jpg', 1337);

--
-- Gegevens worden geëxporteerd voor tabel `api_exercise`
--

INSERT INTO `api_exercise` (`id`, `name`, `description`, `course_id`, `type_id`) VALUES
(1, 'English lesson 1', 'Food', 1, 1),
(2, 'English lesson 2', 'Health', 1, 2),
(3, 'English lesson 3', 'Sports', 1, 3),
(4, 'German lesson 1', 'Basics', 2, 1),
(5, 'German lesson 2', 'Health', 2, 2),
(6, 'German lesson 3', 'Sports', 3, 3),
(7, 'French lesson 1', 'Basics', 3, 1),
(8, 'French lesson 2', 'Health', 3, 2),
(9, 'French lesson 3', 'Sports', 3, 3);

--
-- Gegevens worden geëxporteerd voor tabel `api_exercisetype`
--

INSERT INTO `api_exercisetype` (`id`, `name`, `description`) VALUES
(1, 'Grammar', 'Learn grammar'),
(2, 'Flashcards', 'Learn with flashcards'),
(3, 'Completion', 'Learn with completion exercises');

--
-- Gegevens worden geëxporteerd voor tabel `api_language`
--

INSERT INTO `api_language` (`id`, `name`, `flag`) VALUES
(1, 'English', 'england'),
(2, 'Dutch', 'netherlands'),
(3, 'German', 'germany'),
(4, 'French', 'france'),
(5, 'Russian', 'russia'),
(6, 'Spanish', 'spain');

--
-- Gegevens worden geëxporteerd voor tabel `api_subscription`
--

INSERT INTO `api_subscription` (`id`, `course_id`, `user_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 1, 3),
(4, 3, 1),
(5, 2, 3),
(6, 3, 2);

--
-- Gegevens worden geëxporteerd voor tabel `api_user`
--

INSERT INTO `api_user` (`id`, `email`, `name`, `password`, `distributor`) VALUES
(1, 'piet@hotmail.com', 'piet', 'welkom123', 0),
(2, 'jan@hotmail.com', 'jan', 'welkom123', 1),
(3, 'peter@hotmail.com', 'peter', 'welkom123', 0),
(4, 'sara@hotmail.com', 'sara', 'welkom123', 1),
(5, 'evert@hotmail.com', 'evert', 'welkom123', 0);

--
-- Gegevens worden geëxporteerd voor tabel `django_content_type`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$100000$kEJf41igeCuu$iHOT0wafWzt+SlSOD7N7iPdigUNx5bzVJfz5g8JPyR8=', '2018-05-30 08:00:26.447438', 1, 'root', '', '', 'bertde.boer@hotmail.com', 1, 1, '2018-05-30 07:59:58.949897');

SET FOREIGN_KEY_CHECKS = 1;