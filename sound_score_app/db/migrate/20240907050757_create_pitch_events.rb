class CreatePitchEvents < ActiveRecord::Migration[7.0]
  def change
    create_table :pitch_events do |t|
      t.references :user, null: false, foreign_key: true
      t.references :song, null: false, foreign_key: true

      t.timestamps
    end
  end
end
