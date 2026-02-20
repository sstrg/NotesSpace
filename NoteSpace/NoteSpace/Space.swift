//
//  Space.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import Foundation

struct Space: Identifiable, Codable {
    let id: String
    var name: String
    var description: String
    var creatorId: String
    var adminIds: [String]  
    var memberIds: [String]
    var noteIds: [String]
    var inviteCode: String
    var createdAt: Date
}
