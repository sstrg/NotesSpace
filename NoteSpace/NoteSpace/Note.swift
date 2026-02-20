//
//  Note.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import Foundation

struct Note: Identifiable, Codable {
    let id: String
    var title: String
    var content: String
    var authorId: String
    var authorName: String
    var spaceId: String
    var createdAt: Date
    var updatedAt: Date
}
