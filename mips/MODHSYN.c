#define VOLUME_MAGIC 0x81020409

// Inisialisasi 
void init_audio_device(AudioDevice* dev) {
    memset(dev->buffer, 0, 0x18);  // Clear memory
    
    // Loop manajemen channel
    for (int i = 0; i < 16; i++) {
        Channel* ch = &dev->channels[i];
        if (ch->status != DEVICE_READY) {
            jal_reset_channel(ch);  // 0x7c0
        }
        dev->channel_ptr += 0x38;  // Offset struktur channel
    }
}

// Magic number untuk konversi volume
void set_volume(Channel* ch, uint8_t volume) {
    // Konversi linear ke logarithmic (khas audio)
    uint32_t scaled = (volume & 0xFF) << 7;
    uint32_t result = (scaled * VOLUME_MAGIC) >> 6;
    
    if (ch->current_volume != result) {
        ch->current_volume = result;
        update_hardware_volume(ch);  // 0x99c
    }
}
