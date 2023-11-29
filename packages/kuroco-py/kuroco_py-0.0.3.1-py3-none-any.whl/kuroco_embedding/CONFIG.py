QUERY_KW: str = "vector_search"
VECTOR_SEARCH_MODIFIER: str = "vector_search_modifier"

EMBEDDING_COLUMN_VECTORS: str = "EMBEDDING_COLUMN_VECTORS"

SCORE_DISTANCE_COLUMN_NAME: str = "vector_distance"
LABEL_SCORE_COLUMN_NAME: str = "label_score"
KEYWORDS_SCORE_COLUMN_NAME: str = "keywords_score"

ACCEPTED_LANGUAGES: list = ["eng", "jp", "fr", "es"]

APPRECIATION_DEFINITIONS: dict = {
    "eng": {
        "positive": ["good or useful"],
        "negative": ["not good or useful"],
    },
    "jp": {
       "positive": ["ポジティブ", "ポジティブに", "ポジティブさ", "ポジティブ主義的"],
        "negative": ["ネガティブ", "ネガティブに", "ネガティブさ", "ネガティブ主義的"],
    },
    "fr": {
        "positive": ["bon ou utile"],
        "negative": ["pas bon ou utile"],
    },
    "es": {
        "positive": ["bueno o útil"],
        "negative": ["no bueno o útil"],
    },
}


SENTIMENTS_DEFINITIONS: dict = {
    "eng": {
        "joy": ["a feeling of great happiness"],
        "jealousy": [" feeling of anger or bitterness which someone has when they think that another person is trying to take a lover or friend, or a possession, away from them"],
        "surprise": ["unexpected event, fact, or piece of news"],
        "sadness": ["feeling unhappy, usually because something has happened that you do not like"],
        "anger": [" strong emotion that you feel when you think that someone has behaved in an unfair, cruel, or unacceptable way."],
        "fear": ["unpleasant feeling you have when you think that you are in danger."],
        "disgust": ["a feeling of very strong dislike or disapproval"],
        "trust": ["a feeling of believing in honesty and sincerity into something or someone"],
        "love": ["to like something very much"],
        "disappointment": ["feeling about swomething which is not as good as you had hoped"],
        "like": ["feeling about something as interesting, enjoyable, or attractive"],
        "hate": ["having an extremely strong feeling of dislike for something or someone"],
        "confusion": ["to not know exactly what is happening or what to do"],        
        "hope": ["feeling for something, you want it to be true or to happen, and you usually believe that it is possible or likely."],
        "irony": ["a subtle form of humour which involves saying things that you do not mean."],
    },
    "jp": {
        "joy": ["大きな幸福感"],
        "jealousy": ["他の人が恋人や友達、または物を奪おうとしていると思ったときに生じる怒りや苦い感情"],
        "surprise": ["予期せぬ出来事、事実、またはニュース"],
        "sadness": ["何か嫌なことがあったときに感じる不幸な気持ち"],
        "anger": ["公正でない、残酷でない、または受け入れがたい方法で誰かが行動したときに感じる強い感情"],
        "fear": ["自分が危険にさらされていると思うときに抱く不快な感情"],
        "disgust": ["非常に強い嫌悪感や非難の気持ち"],
        "trust": ["誠実さや正直さを信じる気持ち、またはそれが何かや誰かに向けられる"],
        "love": ["何かを非常に好きである気持ち"],
        "disappointment": ["期待したほど良くないと感じる気持ち"],
        "like": ["何かを面白い、楽しい、または魅力的だと感じる気持ち"],
        "hate": ["何かや誰かに対して非常に強い嫌悪感を抱くこと"],
        "confusion": ["具体的に何が起こっているのか、または何をすべきかが正確にわからない状態"],
        "hope": ["何かに対して、それが真実であるか起こることを望み、通常はそれが可能または起こりそうだと信じる気持ち"],
        "irony": ["言ったこととは逆の意味を含む微妙なユーモアの形式"],
    },
    "fr": {
    "joy": ["un sentiment de grande bonheur"],
    "jealousy": ["sentiment de colère ou d'amertume qu'une personne ressent lorsqu'elle pense qu'une autre personne essaie de lui prendre un amoureux, un ami ou une possession"],
    "surprise": ["événement, fait ou nouvelle inattendu(e)"],
    "sadness": ["sentiment de malheur, généralement parce qu'il s'est passé quelque chose que vous n'aimez pas"],
    "anger": ["émotion intense que l'on ressent lorsqu'on pense que quelqu'un s'est comporté de manière injuste, cruelle ou inacceptable"],
    "fear": ["sentiment désagréable que vous avez lorsque vous pensez que vous êtes en danger"],
    "disgust": ["sentiment de très forte aversion ou désapprobation"],
    "trust": ["sentiment de croire en l'honnêteté et la sincérité envers quelque chose ou quelqu'un"],
    "love": ["aimer quelque chose énormément"],
    "disappointment": ["sentiment à propos de quelque chose qui n'est pas aussi bon que vous l'aviez espéré"],
    "like": ["sentiment envers quelque chose comme étant intéressant, agréable ou attirant"],
    "hate": ["avoir un sentiment extrêmement fort de dégoût envers quelque chose ou quelqu'un"],
    "confusion": ["ne pas savoir exactement ce qui se passe ou que faire"],
    "hope": ["sentiment pour quelque chose que vous voulez voir se réaliser et auquel vous croyez généralement comme étant possible ou probable"],
    "irony": ["une forme subtile d'humour qui consiste à dire des choses que l'on ne pense pas vraiment."],
    },
    "es": {
        "joy": ["un sentimiento de gran felicidad"],
        "jealousy": ["sentimiento de enojo o amargura que alguien siente cuando piensa que otra persona está tratando de quitarle un amante, un amigo o una posesión"],
        "surprise": ["evento, hecho o noticia inesperada"],
        "sadness": ["sentimiento de infelicidad, generalmente porque ha sucedido algo que no te gusta"],
        "anger": ["emoción intensa que sientes cuando piensas que alguien ha actuado de manera injusta, cruel o inaceptable"],
        "fear": ["sentimiento desagradable que tienes cuando piensas que estás en peligro"],
        "disgust": ["sentimiento de aversión o desaprobación muy fuerte"],
        "trust": ["sentimiento de creer en la honestidad y sinceridad hacia algo o alguien"],
        "love": ["gustar mucho algo"],
        "disappointment": ["sentimiento acerca de algo que no es tan bueno como esperabas"],
        "like": ["sentimiento hacia algo como interesante, agradable o atractivo"],
        "hate": ["sentir un odio extremadamente fuerte hacia algo o alguien"],
        "confusion": ["no saber exactamente lo que está sucediendo o qué hacer"],
        "hope": ["sentimiento hacia algo, deseas que sea verdad o que suceda, y generalmente crees que es posible o probable"],
        "irony": ["una forma sutil de humor que implica decir cosas que no se quieren decir realmente."],
    },
}
