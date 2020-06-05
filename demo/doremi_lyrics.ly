\score {
  <<
    \new Voice = "one" {
      \relative {
          \tempo 4 = 110
          c'4. d8 e4. d8 e4 d4 e2
      }
    }
    \new Lyrics \lyricsto "one" {
      \lyricmode {
        Doe a deer a fe male deer
      }
    }
  >>
}
