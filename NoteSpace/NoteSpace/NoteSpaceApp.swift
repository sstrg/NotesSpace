//
//  NoteSpaceApp.swift
//  NoteSpace
//
//  Created by User on 2026-02-19.
//

import SwiftUI

@main
struct NoteSpaceApp: App {
    @StateObject private var dataManager = DataManager.shared
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(dataManager)
        }
    }
}
