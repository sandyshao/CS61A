test = {
  'names': [
    'q3',
    '3'
  ],
  'points': 1,
  'suites': [
    [
      {
        'locked': True,
        'test': """
        >>> positive = make_sentiment(0.2)
        >>> neutral = make_sentiment(0)
        >>> unknown = make_sentiment(None)
        >>> has_sentiment(positive)
        8e50f8b46d3c4b8dd1ed96e8c33acc3d
        # locked
        >>> has_sentiment(neutral)
        8e50f8b46d3c4b8dd1ed96e8c33acc3d
        # locked
        >>> has_sentiment(unknown)
        06a864a242aa6be42c03bcf1f5e0d69f
        # locked
        >>> sentiment_value(positive)
        a7554ae9d78d1e1dd492ab6642cba365
        # locked
        >>> sentiment_value(neutral)
        69a288dfec1127d2c678fda1bde81b60
        # locked
        """,
        'type': 'doctest'
      }
    ]
  ]
}