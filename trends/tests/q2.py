test = {
  'names': [
    'q2',
    '2'
  ],
  'points': 2,
  'suites': [
    [
      {
        'locked': True,
        'test': """
        >>> extract_words("anything else.....not my job")
        5b3fc4bcc5a398dbc96f85718327e1dd
        # locked
        # choice: ['anything', 'else', 'not', 'my', 'job']
        # choice: ['anything', 'else', '.....', 'not', 'my', 'job']
        # choice: ['anything', 'else.....not', 'my', 'job']
        # choice: ['anything', 'else', '.', '.', '.', '.', '.', 'not', 'my', 'job']
        """,
        'type': 'doctest'
      },
      {
        'locked': True,
        'test': """
        >>> extract_words('i love my job. #winning')
        6e97e7f22f47aff383e250cfe195ded8
        # locked
        # choice: ['i', 'love', 'my', 'job', 'winning']
        # choice: ['i', 'love', 'my', 'job.', '#winning']
        # choice: ['i', 'love', 'my', 'job', '.', '#', 'winning']
        # choice: ['i', 'love', 'my', 'job']
        """,
        'type': 'doctest'
      },
      {
        'locked': True,
        'test': """
        >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
        c4a8dde8f2ef1947bfe193f24d80a573
        # locked
        # choice: ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
        # choice: ['make', 'justin', '#', '1', 'by', 'tweeting', '#', 'vma', '#', 'justinbieber']
        # choice: ['make', 'justin', '#', '1', 'by', 'tweeting', '#vma', '#justinbieber']
        # choice: ['make', 'justin', '1', 'by', 'tweeting']
        """,
        'type': 'doctest'
      },
      {
        'locked': True,
        'test': """
        >>> extract_words("paperclips! they're so awesome, cool, & useful!")
        b6b6b6d00361e5f3234f38958b200cbf
        # locked
        # choice: ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
        # choice: ['paperclips!', "they're", 'so', 'awesome,', 'cool,', 'useful!']
        # choice: ['paperclips!', "they're", 'so', 'awesome', 'cool', '&', 'useful']
        # choice: ['paperclips!', 'they', 'so', 'awesome', 'cool', 'and', 'useful']
        """,
        'type': 'doctest'
      },
      {
        'locked': True,
        'test': """
        >>> extract_words('@(cat$.on^#$my&@keyboard***@#*')
        29026c214581d337b7fe73fc258e71f4
        # locked
        # choice: ['cat', 'on', 'my', 'keyboard']
        # choice: ['@', '(', 'cat', '$', '.', 'on', '^', '#', '$', 'my', '&', '@', 'keyboard', '***', '@', '#', '*']
        # choice: ['catonmykeyboard']
        """,
        'type': 'doctest'
      }
    ],
    [
      {
        'never_lock': True,
        'test': """
        >>> extract_words("This.is separated!by@only#non$letter%characters^so&you*need(to)use-white+listing{instead}of black/listing:or'else<you'll>get~the wrong answer")
        ['This', 'is', 'separated', 'by', 'only', 'non', 'letter', 'characters', 'so', 'you', 'need', 'to', 'use', 'white', 'listing', 'instead', 'of', 'black', 'listing', 'or', 'else', 'you', 'll', 'get', 'the', 'wrong', 'answer']
        """,
        'type': 'doctest'
      }
    ]
  ]
}