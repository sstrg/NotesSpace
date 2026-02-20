//
//  AddNoteView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

struct AddNoteView: View {
    let space: Space
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject private var dataManager: DataManager
    
    @State private var title = ""
    @State private var content = ""
    
    var body: some View {
        NavigationView {
            Form {
                TextField("Title", text: $title)
                TextEditor(text: $content)
                    .frame(height: 200)
            }
            .navigationTitle("New Note")
            .navigationBarItems(
                leading: Button("Cancel") { dismiss() },
                trailing: Button("Save") {
                    if let userId = dataManager.currentUser?.id,
                       let username = dataManager.currentUser?.username {
                        dataManager.createNote(
                            title: title,
                            content: content,
                            spaceId: space.id,
                            authorId: userId,
                            authorName: username
                        )
                        dismiss()
                    }
                }
                .disabled(title.isEmpty)
            )
        }
    }
}
