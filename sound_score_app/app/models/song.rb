class Song < ApplicationRecord
  has_many :pitch_events
  has_many :histories
  has_many :song_pitches
end
