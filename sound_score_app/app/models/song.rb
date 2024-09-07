class Song < ApplicationRecord
  has_many :pitch_events
  has_many :histories
end
