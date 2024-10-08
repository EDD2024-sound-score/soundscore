# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2024_09_07_051218) do
  create_table "histories", force: :cascade do |t|
    t.integer "user_id", null: false
    t.integer "song_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.datetime "played_at", null: false
    t.float "score"
    t.text "record"
    t.index ["song_id"], name: "index_histories_on_song_id"
    t.index ["user_id"], name: "index_histories_on_user_id"
  end

  create_table "pitch_events", force: :cascade do |t|
    t.integer "user_id", null: false
    t.integer "song_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.text "pitch", default: "[]", null: false
    t.float "deviation", null: false
    t.index ["song_id"], name: "index_pitch_events_on_song_id"
    t.index ["user_id"], name: "index_pitch_events_on_user_id"
  end

  create_table "song_pitches", force: :cascade do |t|
    t.integer "song_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.text "pitch", default: "[]", null: false
    t.index ["song_id"], name: "index_song_pitches_on_song_id"
  end

  create_table "songs", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "title", null: false
    t.string "artist"
    t.json "pitch", default: {}
    t.string "genre", null: false
  end

  create_table "users", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
  end

  add_foreign_key "histories", "songs"
  add_foreign_key "histories", "users"
  add_foreign_key "pitch_events", "songs"
  add_foreign_key "pitch_events", "users"
  add_foreign_key "song_pitches", "songs"
end
