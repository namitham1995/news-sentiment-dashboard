--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: news_analytics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.news_analytics (
    id integer NOT NULL,
    author character varying(200),
    description character varying(700),
    sentiment_score double precision,
    "timestamp" character varying(20)
);


ALTER TABLE public.news_analytics OWNER TO postgres;

--
-- Name: news_analytics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.news_analytics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.news_analytics_id_seq OWNER TO postgres;

--
-- Name: news_analytics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.news_analytics_id_seq OWNED BY public.news_analytics.id;


--
-- Name: news_analytics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_analytics ALTER COLUMN id SET DEFAULT nextval('public.news_analytics_id_seq'::regclass);


--
-- Data for Name: news_analytics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.news_analytics (id, author, description, sentiment_score, "timestamp") FROM stdin;
1	BBC	Test news	0.7	2025-06-19 14:00
2	BBC	Test news	0.7	2025-06-19 14:00
3	Reuters	Economy is showing signs of recovery after pandemic.	0.6	2025-06-19 10:30
4	CNN	Unemployment rates hit a new low this quarter.	0.8	2025-06-19 11:00
5	Al Jazeera	Political unrest causes market instability.	-0.4	2025-06-19 12:00
6	NDTV	Heavy rains expected in Mumbai this week.	0.1	2025-06-19 13:15
7	BBC	New tech startups are booming in India.	0.7	2025-06-19 14:45
8	Fox News	Inflation fears drive consumer confidence down.	-0.5	2025-06-19 15:30
9	The Hindu	Government launches new green energy project.	0.5	2025-06-19 16:00
10	Times of India	Cricket team wins series against Australia!	0.9	2025-06-19 17:00
11	BBC	Test news	0.7	2025-06-19 14:00
12	BBC	Test news	0.7	2025-06-19 14:00
13	Jessie Yeung, Lex Harvey, Chris Lau, Antoinette Radford, Maureen Chowdhury, Elise Hammond, Aditi Sangal, Tori B. Powell, Olivia Kemp	Trump weighs US options on sixth day of Israel-Iran conflict - CNN	0	2025-06-19 17:53
14	Rob Wile	Federal Reserve interest rate decision June 2025: What to know. - NBC News	0	2025-06-19 17:53
15	Andre Janse Van Vuuren	Oil Rally Builds as Middle East Unrest Deepens: Markets Wrap - Bloomberg.com	0	2025-06-19 17:53
16	Alex Horton, Maham Javaid, Warren P. Strobel	What is the Massive Ordnance Penetrator, the U.S. bunker-busting bomb? - The Washington Post	0	2025-06-19 17:53
17	Sally Brompton	Your daily horoscope: June 18, 2025 - The Globe and Mail	0	2025-06-19 17:53
18	Mitch Fink	Dave Portnoy goes scorched earth on WNBA, Marina Mabrey after Caitlin Clark shove - New York Post	0.13636363636363635	2025-06-19 17:53
19	John Power	Oil prices spike, US stocks fall on Israel-Iran crisis - Al Jazeera	0	2025-06-19 17:53
20	Paul Kasabian	Panthers Beat Oilers to Win Back-to-Back Stanley Cup Titles, Celebrated By NHL Fans - Bleacher Report	0.575	2025-06-19 17:53
21	Heba Farouk Mahfouz, Claire Parker, Victoria Craw	51 Gazans killed waiting for aid, Health Ministry says; IDF reviewing incident - The Washington Post	-0.2	2025-06-19 17:53
22	Emmet  Lyons	Meta 'concerned' by Iran telling citizens to stop using WhatsApp, spokesperson says - CBS News	0	2025-06-19 17:53
23	Eric Crawford	STILL SWINGING! Louisville walks off Oregon State to stay alive in Omaha - WDRB	0.1	2025-06-19 17:53
24	Sophia Cai, Anthony Adragna	Trump extends TikTok deadline again - Politico	0	2025-06-19 17:53
25	Eugene Kim	Amazon employees slam CEO Andy Jassy's memo about AI killing corporate jobs - Business Insider	0	2025-06-19 17:53
26	Gary Fineout	Florida’s GOP skirmish has been dominated by lawmakers. It’s DeSantis’ turn now. - Politico	0	2025-06-19 17:53
27	ABC News	Sean 'Diddy' Combs trial day 29 recap: Jurors watch videos of 'freak-offs' - ABC News	0	2025-06-19 17:53
28	Sarah Ferris	GOP hawks clash with MAGA isolationists as Trump contemplates next steps in Iran - CNN	0	2025-06-19 17:53
29	Liam Doolan	Sonic Racing: CrossWorlds Officially Reveals Nickelodeon Collaboration - Nintendo Life	0	2025-06-23 10:46
30	Steve Hendrix	Israeli strikes on Iran cap dramatic shift in Mideast strategic balance - The Washington Post	-0.4333333333333333	2025-06-23 10:46
31	Guy Chazan	Trump faces backlash from Maga base after strikes on Iran - Financial Times	-0.4	2025-06-23 10:46
32	Courtney Anderson	FedEx founder Fred Smith dies, sources confirm - WREG.com	0	2025-06-23 10:46
33	\N	What we know about US airstrikes on Iran's nuclear facilities - BBC	0	2025-06-23 10:46
34	Yahoo Sports Staff	College World Series 2025 score: LSU's Kade Anderson makes argument for No. 1 pick with shutout win in Game 1 - Yahoo Sports	0.2	2025-06-23 10:46
35	Paul Grein	Sabrina Carpenter, SZA, Ariana Grande Win Multiple Awards at 2025 Kids’ Choice Awards (Full Winners List) - Billboard	0.3833333333333333	2025-06-23 10:46
36	Geoff Grammer / Journal Staff Writer	UFC champ Jon Jones retires, hit with another criminal charge in Albuquerque - Albuquerque Journal	-0.4	2025-06-23 10:46
37	Kathryn Palmer	US bombs Iran: What to know about possible weapon, the 'bunker buster' - USA Today	0	2025-06-23 10:46
38	Gaya Gupta	Minnesota shooting suspect and wife were ‘preppers,’ FBI affidavit says - The Washington Post	0	2025-06-23 10:46
39	\N	Stress hormones: Why quick fixes won't lower our cortisol levels - BBC	0.3333333333333333	2025-06-23 10:46
40	\N	Hall of Famer Dale Earnhardt Jr. wins NASCAR national series debut as crew chief at Pocono - AP News	0.3	2025-06-23 10:46
41	\N	Belarus opposition leader's husband freed from prison - BBC	0	2025-06-23 10:46
42	Anthony Ha	European leaders worry they’re too reliant on U.S. tech - TechCrunch	0	2025-06-23 10:46
43	Daniel Kreps	BTS’ Suga Pens Message to Fans as Military Service Officially Ends: ‘I Really Missed You’ - Rolling Stone	0.05	2025-06-23 10:46
44	Emell Derra Adolphus	Trump Lists Reasons He Deserves Nobel Prize in Epic Meltdown - The Daily Beast	0.05	2025-06-23 10:46
45	Stephen Clark	Psyche keeps its date with an asteroid, but now it’s running in backup mode - Ars Technica	0	2025-06-23 10:46
46	MARIA CHENG, Associated Press	You probably don’t need foods with added protein, nutritionists say - NewsNation	0	2025-06-23 10:46
\.


--
-- Name: news_analytics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.news_analytics_id_seq', 46, true);


--
-- Name: news_analytics news_analytics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.news_analytics
    ADD CONSTRAINT news_analytics_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

