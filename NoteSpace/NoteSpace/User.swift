//
//  User.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import Foundation

struct User: Identifiable, Codable {
    let id: String
    var email: String
    var username: String
    var password: String // Добавляем пароль
    var spaceIds: [String]
}
