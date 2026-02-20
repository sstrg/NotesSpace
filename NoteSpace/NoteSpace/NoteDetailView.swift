//
//  NoteDetailView.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

struct NoteDetailView: View {
    let note: Note
    @EnvironmentObject private var dataManager: DataManager
    @State private var isEditing = false
    @State private var editedTitle = ""
    @State private var editedContent = ""
    
    var body: some View {
        if isEditing {
            editView
        } else {
            detailView
        }
    }
    
    var detailView: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 15) {
                Text(note.title)
                    .font(.largeTitle)
                    .fontWeight(.bold)
                
                HStack {
                    Text("By \(note.authorName)")
                    Spacer()
                    Text(note.updatedAt, style: .date)
                }
                .font(.caption)
                .foregroundColor(.gray)
                
                Divider()
                
                Text(note.content)
                    .font(.body)
            }
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                if note.authorId == dataManager.currentUser?.id {
                    Button("Edit") {
                        editedTitle = note.title
                        editedContent = note.content
                        isEditing = true
                    }
                }
            }
        }
    }
    
    var editView: some View {
        Form {
            TextField("Title", text: $editedTitle)
            TextEditor(text: $editedContent)
                .frame(height: 300)
        }
        .navigationTitle("Edit Note")
        .navigationBarItems(
            leading: Button("Cancel") {
                isEditing = false
            },
            trailing: Button("Save") {
                dataManager.updateNote(
                    noteId: note.id,
                    title: editedTitle,
                    content: editedContent
                )
                isEditing = false
            }
        )
    }
}
